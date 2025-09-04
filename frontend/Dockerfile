FROM node:20-alpine

WORKDIR /app

# Copy package.json and lock files
COPY frontend/package.json frontend/package-lock.json* frontend/yarn.lock* frontend/pnpm-lock.yaml* ./

RUN npm ci

# Copy all source
COPY frontend . 

COPY frontend/.env.production ./
# Build with Render env vars
RUN npm run build

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]
