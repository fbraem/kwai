/**
 * Function to get the url for a hero image of an application.
 */
export const heroImage = (await import('../../images/hero.jpg')).default;
const images = import.meta.glob('../../images/hero*.jpg');
export function getHeroImageUrl(applicationName: string) {
  for (const image in images) {
    const pathParts = image.split('/');
    if (pathParts[pathParts.length - 1] === `hero_${applicationName}.jpg`) {
      return image;
    }
  }
  // Fallback to the default.
  return heroImage;
}
