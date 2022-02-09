# 2. use server side sessions with redis

Date: 2022-01-31

## Status

Accepted

## Context

So far the session data of the user is stored in a cookie using Flask session. The cookie has a size limit of 4 kb and therefore this limits the size of the data in the session. To be independent of the cookie size, we want to use server side session data.
You can find the internal Tech Spec [here](https://digitalservice4germany.atlassian.net/wiki/spaces/STL/pages/174424075/2022-01+Cookie-Limit)

## Decision

We use a server side session stored in a redis database. 

## Consequences

Sensitive data input like the FSC should not be stored on the server. Sometimes this data needs to be shown to the user on different pages and therefore was part of the session. After the change to the server side session sensitive information should be stored in a separate cookie.

Therefore, we will have the session stored in redis and a separate cookie for information outside of the tax declaration flow. **Note:** The cookie uses the session provided by flask. However, we will refer to the data in redis as the session and the data in the cookie as the cookie data.

To mitigate the risk of data leakage from the redis database the data is stored encrypted and a TTL is set to remove outdated session data.
