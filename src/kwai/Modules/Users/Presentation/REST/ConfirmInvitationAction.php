<?php
/**
 * @package Modules
 * @subpackage Users
 */
declare(strict_types=1);

namespace Kwai\Modules\Users\Presentation\REST;

use Kwai\Core\Infrastructure\Presentation\Responses\NotFoundResponse;
use Kwai\Core\Infrastructure\Presentation\Responses\ResourceResponse;
use Kwai\Core\Infrastructure\Presentation\Responses\SimpleResponse;
use Kwai\Core\Domain\Exceptions\UnprocessableException;
use Kwai\Core\Infrastructure\Presentation\Action;
use Kwai\Core\Infrastructure\Repositories\RepositoryException;
use Kwai\Modules\Users\Domain\Exceptions\UserInvitationNotFoundException;
use Kwai\Modules\Users\Infrastructure\Repositories\UserAccountDatabaseRepository;
use Kwai\Modules\Users\Infrastructure\Repositories\UserInvitationDatabaseRepository;
use Kwai\Modules\Users\Presentation\Transformers\UserAccountTransformer;
use Kwai\Modules\Users\UseCases\ConfirmInvitation;
use Kwai\Modules\Users\UseCases\ConfirmInvitationCommand;
use Nette\Schema\Expect;
use Nette\Schema\Processor;
use Nette\Schema\ValidationException;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;

/**
 * Class ConfirmInvitationAction
 *
 * Action to confirm an invitation.
 */
class ConfirmInvitationAction extends Action
{
    /**
     * Create a command from the request data
     * @param array $data
     * @return ConfirmInvitationCommand
     */
    private function createCommand(array $data): ConfirmInvitationCommand
    {
        $schema = Expect::structure([
            'data' => Expect::structure([
                'type' => Expect::string(),
                'attributes' => Expect::structure([
                    'remark' => Expect::string(),
                    'first_name' => Expect::string()->required(),
                    'last_name' => Expect::string()->required(),
                    'email' => Expect::string()->required(),
                    'password' => Expect::string()->required()
                ])
            ])
        ]);

        $processor = new Processor();
        $normalized = $processor->process($schema, $data);

        $command = new ConfirmInvitationCommand();
        $command->firstName = $normalized->data->attributes->first_name;
        $command->lastName = $normalized->data->attributes->last_name;
        $command->email = $normalized->data->attributes->email;
        $command->remark = $normalized->data->attributes->remark ?? null;
        $command->password = $normalized->data->attributes->password;

        return $command;
    }

    /**
     * @param ServerRequestInterface $request
     * @param ResponseInterface $response
     * @param array $args
     * @return ResponseInterface
     */
    public function __invoke(
        ServerRequestInterface $request,
        ResponseInterface $response,
        array $args
    ): ResponseInterface {
        try {
            $command = $this->createCommand($request->getParsedBody());
            $command->uuid = $args['uuid'];
        } catch (ValidationException $ve) {
            return (new SimpleResponse(422, $ve->getMessage()))($response);
        }

        try {
            $database = $this->getContainerEntry('pdo_db');
            $userAccount = ConfirmInvitation::create(
                new UserInvitationDatabaseRepository($database),
                new UserAccountDatabaseRepository($database)
            )($command);
        } catch (UnprocessableException $e) {
            return (new SimpleResponse(422, $e->getMessage()))($response);
        } catch (UserInvitationNotFoundException) {
            return (new NotFoundResponse('User invitation does not exist'))($response);
        } catch (RepositoryException $e) {
            $this->logException($e);
            return (
                new SimpleResponse(500, 'A repository exception occurred.')
            )($response);
        }

        return (new ResourceResponse(
            UserAccountTransformer::createForItem($userAccount)
        ))($response);
    }
}
