FROM node:24-bookworm-slim AS runtime
ENV NODE_ENV=production GENESIS_RUNTIME_MODE=dormant
WORKDIR /app
COPY package.json package-lock.json .npmrc ./
RUN npm ci --omit=dev && npm cache clean --force
COPY core ./core
COPY runtime ./runtime
COPY server ./server
COPY config ./config
COPY research/genesis-brain-spec-v0.2 ./research/genesis-brain-spec-v0.2
COPY data ./data
COPY SCIENCE.md ARCHITECTURE.md README.md ./
USER node
EXPOSE 3001
CMD ["node", "runtime/main.ts"]
