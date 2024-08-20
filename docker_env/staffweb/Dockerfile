FROM registry.cn-zhangjiakou.aliyuncs.com/dvadmin-pro/dvadmin3-base-web:16.19-alpine
WORKDIR /staffweb/
COPY staffweb/. .
RUN npm install -g pnpm@latest-8 --registry https://registry.npmmirror.com
RUN pnpm install --registry https://registry.npmmirror.com
RUN pnpm build

FROM nginx:alpine
COPY ./docker_env/nginx/mystaffweb.conf /etc/nginx/conf.d/my.conf
COPY --from=0 /staffweb/dist /usr/share/nginx/html
