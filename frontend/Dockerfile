FROM node:22-alpine AS builder
WORKDIR /app
ENV COREPACK_NPM_REGISTRY=https://registry.npmmirror.com
RUN corepack enable
RUN corepack prepare yarn@1.22.22 --activate
COPY package.json yarn.lock ./
RUN sed -i 's#https://registry.yarnpkg.com/#https://registry.npmmirror.com/#g' yarn.lock \
    && yarn install --frozen-lockfile --registry https://registry.npmmirror.com
COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
