declare module "@kwai/config" {
    const website: {
        title: string
        copyright: string
        email: string,
        url: string,
    };
}
declare module "@kwai/config" {
    const portal: {
        social_media: [{
            title: string,
            account: string,
            icon: string,
            url: string,
        }],
        promotion: string[]
    };
}
declare module "@kwai/config" {
    const api: {
        base_url: string
    };
}
