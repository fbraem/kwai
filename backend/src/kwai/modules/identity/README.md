# Identity and Access Management module

## Authenticate User

Use case for authenticating a user. When a user is successfully authenticated this use case will return a refresh token. 

```mermaid
sequenceDiagram
    API->>AuthenticateUser: execute
    AuthenticateUser->>UserAccountRepository: get_user_by_email
    break when the user with the given email doesnot exist
        UserAccountRepository->>AuthenticateUser: raise UserAccountNotFoundException
    end
    UserAccountRepository-->>AuthenticateUser: user_account
    break when the user is revoked
        AuthenticateUser->>API: raise AuthenticationException
    end
    AuthenticateUser->>UserAccount: login
    break when password is wrong
        AuthenticateUser->>API: raise AuthenticationException
    end
    AuthenticateUser->>AccessTokenRepository: create
    AuthenticateUser->>RefreshTokenRepository: create
    AuthenticateUser-->>API: << return >>
```

## Logout

## Mail User Recovery

## Recover User

## Refresh Token

Use case for refreshing the access token. On each request, also a new refresh token will be returned.

```mermaid
sequenceDiagram
    API->>RefreshAccessToken: execute
    RefreshAccessToken->>RefreshTokenRepository: get_by_token_identifier
    break when the token with the given identifier doesnot exist
        RefreshTokenRepository->>RefreshAccessToken: raise RefreshTokenNotFoundException
    end
    RefreshTokenRepository-->>RefreshToken: << create >>
    RefreshToken-->>AccessToken: << create >>
    AccessToken-->>UserAccount: << create >> 
    RefreshToken-->>RefreshAccessToken: << return >>
    break when refresh token is expired
        RefreshAccessToken->>API: raise AuthenticationException
    end
    break when refresh token is revoked
        RefreshAccessToken->>API: raise AuthenticationException
    end
    break when user is revoked
        RefreshAccessToken->>API: raise AuthenticationException
    end
    RefreshAccessToken->>AccessToken: revoke
    RefreshAccessToken->>RefreshToken: revoke
    RefreshAccessToken->>RefreshTokenRepository: update
    RefreshAccessToken->>AccessTokenRepository: update
    RefreshAccessToken-->>AccessToken: << create >>
    RefreshAccessToken->>AccessTokenRepository: create
    RefreshAccessToken-->>RefreshToken: << create >>
    RefreshAccessToken->>RefreshTokenRepository: create
    RefreshToken-->>API: << return >>
```
