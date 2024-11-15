FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# 使用国内镜像源，不知道有没有用
RUN npm install @vue/cli@5.0.8 -g --registry=https://registry.npmmirror.com

COPY package.json .
COPY package-lock.json .
RUN npm install

CMD ["npm", "run", "serve"]