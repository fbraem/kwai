<?php
/**
 * @package
 * @subpackage
 */
declare(strict_types=1);

namespace Kwai\Core\Infrastructure\Dependencies;

use Kwai\Core\Infrastructure\Converter\ConverterFactory;
use Kwai\Core\Infrastructure\Converter\MarkdownConverter;
use Kwai\Core\Domain\ValueObjects\DocumentFormat;

/**
 * Class ConvertDependency
 */
class ConvertDependency implements Dependency
{
    public function __invoke(array $settings)
    {
        $factory = new ConverterFactory();
        $factory->register((string) DocumentFormat::MARKDOWN(), MarkdownConverter::class);
        return $factory;
    }
}
