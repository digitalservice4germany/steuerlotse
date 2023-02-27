FROM node:19 as node

WORKDIR /app/client

RUN yarn install

EXPOSE 3000

CMD ["yarn","start"]