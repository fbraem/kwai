<?php
/**
 * @package Modules
 * @subpackage Trainings
 */
declare(strict_types=1);

namespace Kwai\Modules\Trainings\UseCases;

/**
 * Class UpdateDefinitionCommand
 *
 * Command for the use case Update Definition
 */
class UpdateDefinitionCommand
{
    /**
     * The id of the definition to update
     */
    public int $id;

    /**
     * The name of the definition
     */
    public string $name;

    /**
     * The description of the definition
     */
    public string $description;

    /**
     * The id of a season
     */
    public ?int $season_id;

    /**
     * The id of a team
     */
    public ?int $team_id;

    /**
     * The weekday (1 = monday, ...)
     */
    public int $weekday;

    /**
     * The start time (HH:MM)
     */
    public string $start_time;

    /**
     * The end time (HH:MM)
     */
    public string $end_time;

    /**
     * The timezone for the start/end time
     */
    public string $time_zone;

    /**
     * Is this definition active?
     */
    public bool $active;

    /**
     * The location
     */
    public string $location;

    /**
     * A remark
     */
    public string $remark;
}
