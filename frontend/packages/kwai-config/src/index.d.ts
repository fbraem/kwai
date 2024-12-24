declare module '@kwai/config' {
    const website: {
        title: string,
        copyright: string,
        email: string,
        url: string,
    };
    const contact: {
        street: string,
        city: string,
        email: string,
    };
    const portal: {
        social_media: [{
            title: string,
            account: string,
            icon: string,
            url: string,
            text: string,
        }],
        links: [{
            title: string,
            url: string,
        }],
        promotion: string[],
        promotion_footer: string[],
    };
    const api: {
        base_url: string
    };
}
