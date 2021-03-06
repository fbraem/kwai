<?php
/**
 * @package Modules
 * @subpackage Trainings
 */
declare(strict_types=1);

namespace Kwai\Modules\Trainings\Presentation\Transformers;

use Kwai\Core\Domain\Entity;
use Kwai\Core\Domain\ValueObjects\Event;
use Kwai\Core\Domain\ValueObjects\Text;
use Kwai\Core\Infrastructure\Converter\ConverterFactory;
use Kwai\Modules\Trainings\Domain\Training;
use League\Fractal;

/**
 * Class TrainingTransformer
 *
 * Transforms a Training entity to JSONAPI
 */
class TrainingTransformer extends Fractal\TransformerAbstract
{
    private static string $type = 'trainings';

    private ConverterFactory $converterFactory;

    protected $defaultIncludes = [
        'definition',
        'coaches',
        'teams',
        'presences'
    ];

    /**
     * Create a single resource of a Training entity.
     *
     * @param Entity<Training> $training
     * @param ConverterFactory $converterFactory
     * @return Fractal\Resource\Item
     */
    public static function createForItem(
        Entity $training,
        ConverterFactory $converterFactory
    ): Fractal\Resource\Item {
        return new Fractal\Resource\Item(
            $training,
            new self($converterFactory),
            self::$type
        );
    }

    /**
     * Create a collection of resources for a list of trainings.
     *
     * @param iterable         $trainings
     * @param ConverterFactory $converterFactory
     * @return Fractal\Resource\Collection
     */
    public static function createForCollection(
        iterable $trainings,
        ConverterFactory $converterFactory
    ): Fractal\Resource\Collection {
        return new Fractal\Resource\Collection(
            $trainings,
            new self($converterFactory),
            self::$type
        );
    }

    /**
     * TrainingTransformer constructor.
     *
     * @param ConverterFactory $converterFactory
     */
    private function __construct(ConverterFactory $converterFactory)
    {
        $this->converterFactory = $converterFactory;
    }

    /**
     * @param Entity<Training> $training
     * @return Fractal\Resource\Item|null
     */
    public function includeDefinition(Entity $training)
    {
        /* @var Training $training */
        $definition = $training->getDefinition();
        if ($definition) {
            return DefinitionTransformer::createForItem($definition);
        }
        return null;
    }

    /**
     * @param Entity<Training> $training
     */
    public function includePresences(Entity $training)
    {
        //TODO: return presences
    }

    /**
     * @param Entity<Training> $training
     * @return Fractal\Resource\Collection|null
     */
    public function includeTeams(Entity $training)
    {
        /* @var Training $training */
        $teams = $training->getTeams();
        if ($teams->count() > 0) {
            return TeamTransformer::createForCollection($teams);
        }
        return null;
    }

    /**
     * @param Entity<Training> $training
     * @return Fractal\Resource\Collection|null
     */
    public function includeCoaches(Entity $training)
    {
        /* @var Training $training */
        $coaches = $training->getCoaches();
        if ($coaches->count() > 0) {
            return CoachTransformer::createForCollection($coaches);
        }
        return null;
    }

    /**
     * Transform the training to JSONAPI structure.
     *
     * @param Entity<Training> $training
     * @return array
     */
    public function transform(Entity $training): array
    {
        /* @var Training $training */
        $traceableTime = $training->getTraceableTime();

        /* @var Event $event */
        $event = $training->getEvent();
        $result = [
            'id' => strval($training->id()),
            'created_at' => strval($traceableTime->getCreatedAt()),
            'remark' => $training->getRemark(),
            'event' => [
                'start_date' => strval($event->getStartDate()),
                'end_date' => strval($event->getEndDate()),
                'time_zone' => $event->getStartDate()->getTimezone(),
                'location' => strval($event->getLocation()),
                'cancelled' => $event->isCancelled(),
                'active' => $event->isActive(),
            ],
            'contents' => $training->getText()->map(function (Text $text) {
                $converter = $this->converterFactory
                    ->createConverter((string) $text->getFormat())
                ;
                return [
                    'locale' => $text->getLocale(),
                    'title' => $text->getTitle(),
                    'summary' => $text->getSummary(),
                    'content' => $text->getContent(),
                    'html_summary' => $converter->convert($text->getSummary()),
                    'html_content' => $converter->convert($text->getContent() ?? ''),
                ];
            })->toArray()
        ];
        $result['updated_at'] = $traceableTime->isUpdated()
            ? strval($traceableTime->getUpdatedAt())
            : null
        ;

        return $result;
    }
}
