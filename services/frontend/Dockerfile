FROM node:24-alpine3.24

WORKDIR /app 

COPY package*.json ./

# Uses the /root/.npm cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm install

#  Uses the /var/cache/apk cache mount
RUN --mount=type=cache,target=/var/cache/apk \
    apk add curl


RUN chown -R node:node /app

COPY . .

USER node

EXPOSE 3000

HEALTHCHECK  --interval=10s --timeout=2s --start-period=5s --start-interval=1s \
  CMD sh /app/healthcheck.sh || exit 1

CMD ["node", "app.js"]
