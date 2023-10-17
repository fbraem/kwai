declare module '@kwai/config' {
    const website: {
        title: string
        copyright: string
        email: string,
        url: string,
    };
    const portal: {
        social_media: [{
            title: string,
            account: string,
            icon: string,
            url: string,
        }],
        promotion: string[]
    };
    const api: {
        base_url: string
    };
}
