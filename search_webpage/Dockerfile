FROM node:18


WORKDIR /search_webpage

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run start"]