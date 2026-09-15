FROM node:24-bookworm-slim AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY package.json package-lock.json .npmrc ./
RUN npm ci --omit=dev && npm cache clean --force
COPY core ./core
COPY runtime ./runtime
COPY server/store.ts ./server/store.ts
COPY data ./data
COPY SCIENCE.md ARCHITECTURE.md README.md ./
USER node
EXPOSE 3001
CMD ["node", "runtime/main.ts"]
