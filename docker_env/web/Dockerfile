FROM registry.cn-zhangjiakou.aliyuncs.com/dvadmin-pro/dvadmin3-base-web:16.19-alpine
WORKDIR /web/
COPY web/. .
RUN npm install -g pnpm@latest-8 --registry https://registry.npmmirror.com
RUN pnpm install  --registry https://registry.npmmirror.com
RUN pnpm build

FROM nginx:alpine
COPY ./docker_env/nginx/my.conf /etc/nginx/conf.d/my.conf
COPY --from=0 /web/dist /usr/share/nginx/html
