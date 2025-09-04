# -------------------------------------------
# Build stage
# -------------------------------------------
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package manifests
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install dependencies
RUN npm ci

# Copy the rest of the source code
COPY . .

# Build Next.js app
RUN npm run build

# -------------------------------------------
# Production stage
# -------------------------------------------
FROM node:20-alpine AS runner

WORKDIR /app

# Copy package manifests
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install only production dependencies
RUN npm ci --omit=dev

# Copy built files from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.js ./next.config.js

# Expose port 3000 (Render expects the service to listen here)
EXPOSE 3000

# Set NODE_ENV
ENV NODE_ENV=production

# Start the Next.js app
CMD ["npm", "start"]
