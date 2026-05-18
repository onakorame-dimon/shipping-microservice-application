FROM node:24-alpine

COPY ./frontend /app 

WORKDIR /app

RUN npm  install 
RUN apk add --no-cache curl  
RUN chown -R node:node /app

USER node

EXPOSE 3000

HEALTHCHECK  --interval=10s --timeout=2s --start-period=5s --start-interval=1s \
  CMD curl -I localhost:3000 || exit 1

CMD ["node", "app.js"]
