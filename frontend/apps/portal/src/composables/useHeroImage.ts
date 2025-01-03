/**
 * Function to get the url for a hero image of an application.
 */
export const heroImage = new URL('../../images/hero.jpg', import.meta.url).href;
const images = import.meta.glob(
  '../../images/hero*.jpg',
  {
    eager: true,
    query: '?url',
    import: 'default'
  },
);
export function getHeroImageUrl(applicationName: string) {
  for (const image in images) {
    const pathParts = image.split('/');
    if (pathParts[pathParts.length - 1] === `hero_${applicationName}.jpg`) {
      return images[image];
    }
  }
  // Fallback to the default.
  return heroImage;
}
