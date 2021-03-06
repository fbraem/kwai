<?php
/**
 * @package Modules
 * @subpackage Trainings
 */
declare(strict_types=1);

namespace Kwai\Modules\Trainings\Presentation\REST;

use Kwai\Core\Infrastructure\Presentation\Action;
use Kwai\Core\Infrastructure\Presentation\Responses\NotFoundResponse;
use Kwai\Core\Infrastructure\Presentation\Responses\ResourceResponse;
use Kwai\Core\Infrastructure\Presentation\Responses\SimpleResponse;
use Kwai\Core\Infrastructure\Repositories\RepositoryException;
use Kwai\Modules\Trainings\Domain\Exceptions\TrainingNotFoundException;
use Kwai\Modules\Trainings\Infrastructure\Repositories\TrainingDatabaseRepository;
use Kwai\Modules\Trainings\Presentation\Transformers\PresenceTransformer;
use Kwai\Modules\Trainings\UseCases\GetTraining;
use Kwai\Modules\Trainings\UseCases\GetTrainingCommand;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

/**
 * Class GetTrainingPresencesAction
 */
class GetTrainingPresencesAction extends Action
{
    /**
     * @inheritDoc
     */
    public function __invoke(Request $request, Response $response, array $args)
    {
        $command = new GetTrainingCommand();
        $command->id = (int) $args['id'];
        $command->withPresences = true;

        $database = $this->getContainerEntry('pdo_db');

        try {
            $training = GetTraining::create(
                new TrainingDatabaseRepository($database)
            )($command);
        } catch (RepositoryException $re) {
            $this->logException($re);
            return (
            new SimpleResponse(500, 'A repository exception occurred.')
            )($response);
        } catch (TrainingNotFoundException) {
            return (new NotFoundResponse('Training not found'))($response);
        }

        /** @noinspection PhpUndefinedMethodInspection */
        $resource = PresenceTransformer::createForCollection(
            $training->getPresences()
        );

        return (new ResourceResponse(
            $resource
        ))($response);
    }
}
