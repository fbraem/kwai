# Welcome to the frontend of kwai.

The frontend consists of several single page applications. [Vue](https://vuejs.org) is used as JavaScript framework.
The frontend code is written with [Typescript](https://www.typescriptlang.org/).

The code is structured as a mono repository. It contains applications
and libraries.

## Install

### Prerequisites

Clone the repository to your system.

[npm](https://www.npmjs.com/) is used as packaging and dependency management tool.
Make sure it is available.

Use npm to install all dependencies:

`npm install`

### Configuration

The frontend uses a config package.

## Development

A development version of the frontend can be started:

`npm run dev`

[Vite](https://vitejs.dev/) is the local development server.
Each application will have a vite server. To serve all applications
from one url, Nginx can be used as reverse proxy. Use the following
configuration for Nginx:

````
server {
  listen 80;
  include /etc/nginx/mime.types;

  proxy_http_version  1.1;
  proxy_set_header Upgrade $http_upgrade; # allow websockets
  proxy_set_header Connection "upgrade";
  proxy_set_header Host $http_host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header X-Forwarded-Host $host:$server_port;
      
  location /author {
           proxy_pass http://localhost:3001/author;
  }
  location /auth {
           proxy_pass http://localhost:3002/auth;
  }
  location / {
           proxy_pass http://localhost:3000/;
  }
}
````

## Build

To create a production version of the frontend:

`npm run build`

This will create dist folders in each application.
