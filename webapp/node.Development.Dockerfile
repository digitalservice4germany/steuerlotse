FROM node:14 as node

WORKDIR /app/client

RUN yarn install
RUN npm install

EXPOSE 3000

CMD ["yarn","start"]