<?php
/**
 * @package
 * @subpackage
 */
declare(strict_types=1);


namespace Kwai\Core\Infrastructure\Repositories;

use Illuminate\Support\Collection;
use Kwai\Core\Infrastructure\Database\QueryException;

/**
 * Interface Query
 *
 * Interface for a query object.
 */
interface Query
{
    /**
     * Execute the query for counting the number of results.
     *
     * @return int
     * @throws QueryException
     */
    public function count(): int;

    /**
     * Execute the query.
     *
     * @param int|null $limit
     * @param int|null $offset
     * @return Collection
     * @throws QueryException
     */
    public function execute(?int $limit = null, ?int $offset = null): Collection;
}
