<?php
/**
 * @package Modules
 * @subpackage Users
 */
declare(strict_types = 1);

namespace Kwai\Modules\Users\Presentation\REST;

use Kwai\Core\Infrastructure\Presentation\Responses\NotAuthorizedResponse;
use Kwai\Core\Infrastructure\Presentation\Responses\SimpleResponse;
use Firebase\JWT\JWT;
use Kwai\Core\Infrastructure\Presentation\Action;
use Kwai\Core\Infrastructure\Repositories\RepositoryException;
use Kwai\Modules\Users\Domain\Exceptions\AuthenticationException;
use Kwai\Modules\Users\Domain\Exceptions\UserAccountNotFoundException;
use Kwai\Modules\Users\Infrastructure\Repositories\AccessTokenDatabaseRepository;
use Kwai\Modules\Users\Infrastructure\Repositories\RefreshTokenDatabaseRepository;
use Kwai\Modules\Users\Infrastructure\Repositories\UserAccountDatabaseRepository;
use Kwai\Modules\Users\UseCases\AuthenticateUser;
use Kwai\Modules\Users\UseCases\AuthenticateUserCommand;
use Nette\Schema\Expect;
use Nette\Schema\Processor;
use Nette\Schema\ValidationException;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

/**
 * Class LoginAction
 *
 * Action to login a user with email/pwd and return access- and refreshtoken on success.
 */
class LoginAction extends Action
{
    /**
     * Create a command from the request data
     * @param array $data
     * @return AuthenticateUserCommand
     */
    private function createCommand(array $data): AuthenticateUserCommand
    {
        $schema = Expect::structure([
            'username' => Expect::string()->required(),
            'password' => Expect::string()->required(),
        ])->otherItems(Expect::string());
        $processor = new Processor();
        $normalized = $processor->process($schema, $data);

        $command = new AuthenticateUserCommand();
        $command->email = $normalized->username;
        $command->password = $normalized->password;

        return $command;
    }

    /**
     * Login the user and return an access- and refreshtoken.
     * @param  Request  $request  The current HTTP request
     * @param  Response $response The current HTTP response
     * @param  string[] $args     Route???s named placeholders
     * @return Response
     * @SuppressWarnings(PHPMD.UnusedFormalParameter)
     */
    public function __invoke(
        Request $request,
        Response $response,
        array $args
    ): Response {
        try {
            $command = $this->createCommand($request->getParsedBody());
        } catch (ValidationException $ve) {
            return (new SimpleResponse(422, $ve->getMessage()))($response);
        }

        try {
            $database = $this->getContainerEntry('pdo_db');
            $refreshToken = AuthenticateUser::create(
                new UserAccountDatabaseRepository($database),
                new AccessTokenDatabaseRepository($database),
                new RefreshTokenDatabaseRepository($database)
            )($command);
        } catch (AuthenticationException) {
            return (new NotAuthorizedResponse('Authentication failed'))($response);
        } catch (RepositoryException $e) {
            $this->logException($e);
            return (
                new SimpleResponse(500, 'A repository exception occurred.')
            )($response);
        } catch (UserAccountNotFoundException) {
            return (new NotAuthorizedResponse('Unknown user'))($response);
        }

        $secret = $this->getContainerEntry('settings')['security']['secret'];
        $algorithm = $this->getContainerEntry('settings')['security']['algorithm'];

        /** @noinspection PhpUndefinedMethodInspection */
        $accessToken = $refreshToken->getAccessToken();
        /** @noinspection PhpUndefinedMethodInspection */
        $data = [
            'access_token' => JWT::encode(
                [
                    'iat' => $accessToken->getTraceableTime()->getCreatedAt()->format('U'),
                    'exp' => $accessToken->getExpiration()->format('U'),
                    'jti' => strval($accessToken->getIdentifier()),
                    'sub' => strval($accessToken->getUserAccount()->getUser()->getUuid()),
                    'scope' => []
                ],
                $secret,
                $algorithm
            ),
            'refresh_token' => JWT::encode(
                [
                    'iat' => $refreshToken->getTraceableTime()->getCreatedAt()->format('U'),
                    'exp' => $refreshToken->getExpiration()->format('U'),
                    'jti' => strval($refreshToken->getIdentifier())
                ],
                $secret,
                $algorithm
            ),
            'expires' => strval($accessToken->getExpiration())
        ];

        $response->getBody()->write(json_encode($data, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
        return $response
            ->withStatus(201)
            ->withHeader("Content-Type", "application/json")
        ;
    }
}
