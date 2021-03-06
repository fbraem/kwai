<?php
/**
 * @package Modules
 * @subpackage Users
 */
declare(strict_types=1);

namespace Kwai\Modules\Users\Infrastructure\Repositories;

use Illuminate\Support\Collection;
use Kwai\Core\Infrastructure\Database\DatabaseQuery;
use Kwai\Modules\Users\Infrastructure\Tables;
use Kwai\Modules\Users\Repositories\RuleQuery;
use function Latitude\QueryBuilder\alias;
use function Latitude\QueryBuilder\field;
use function Latitude\QueryBuilder\on;

/**
 * Class RuleDatabaseQuery
 */
class RuleDatabaseQuery extends DatabaseQuery implements RuleQuery
{
    /**
     * @inheritDoc
     */
    protected function initQuery(): void
    {
        /** @noinspection PhpUndefinedFieldInspection */
        $this->query
            ->from((string) Tables::RULES())
            ->join(
                (string) Tables::RULE_ACTIONS(),
                on(
                    Tables::RULES()->action_id,
                    Tables::RULE_ACTIONS()->id
                )
            )
            ->join(
                (string) Tables::RULE_SUBJECTS(),
                on(
                    Tables::RULES()->subject_id,
                    Tables::RULE_SUBJECTS()->id
                )
            )
        ;
    }

    /**
     * @inheritDoc
     */
    protected function getColumns(): array
    {
        $aliasRulesFn = Tables::RULES()->getAliasFn();

        /** @noinspection PhpUndefinedFieldInspection */
        return [
            $aliasRulesFn('id'),
            $aliasRulesFn('name'),
            $aliasRulesFn('remark'),
            $aliasRulesFn('created_at'),
            $aliasRulesFn('updated_at'),
            // Trick the mapper with the 'rules_' prefix ...
            alias(
                Tables::RULE_ACTIONS()->name,
                Tables::RULES()->getAlias('action')
            ),
            // Trick the mapper with the 'rules_' prefix ...
            alias(
                Tables::RULE_SUBJECTS()->name,
                Tables::RULES()->getAlias('subject')
            )
        ];
    }

    /**
     * @inheritDoc
     */
    public function filterById(int ...$id): RuleQuery
    {
        /** @noinspection PhpUndefinedFieldInspection */
        $this->query->andWhere(
            field(Tables::RULES()->id)->in(...$id)
        );
        return $this;
    }

    /**
     * @inheritDoc
     */
    public function filterBySubject(string $subject): RuleQuery
    {
        /** @noinspection PhpUndefinedFieldInspection */
        $this->query->andWhere(
            field(Tables::RULE_SUBJECTS()->name)->eq($subject)
        );
        return $this;
    }

    public function execute(?int $limit = null, ?int $offset = null): Collection
    {
        $rows = parent::walk($limit, $offset);

        $rules = new Collection();
        $filters = new Collection([
            Tables::RULES()->getAliasPrefix()
        ]);

        foreach ($rows as $row) {
            [ $rule ] = $row->filterColumns($filters);
            $rules->put($rule->get('id'), $rule);
        }

        return $rules;
    }
}
