FROM node:18


WORKDIR /search_webpage

COPY ./package.json ./

RUN npm install

COPY . .

EXPOSE 3000
ENTRYPOINT [ "npm" ]
CMD ["start"]