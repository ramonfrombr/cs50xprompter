# ----------------------
# Build Stage
# ----------------------
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and lock files
COPY frontend/package.json frontend/package-lock.json* frontend/yarn.lock* frontend/pnpm-lock.yaml* ./

# Install all dependencies (including dev)
RUN npm ci

# Copy source code
COPY frontend .

# Build Next.js app
RUN npm run build

# ----------------------
# Production Stage
# ----------------------
FROM node:20-alpine AS runner

WORKDIR /app

# Copy package.json and install only production dependencies
COPY frontend/package.json frontend/package-lock.json* frontend/yarn.lock* frontend/pnpm-lock.yaml* ./
RUN npm ci --omit=dev

# Copy built files from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Set environment
ENV NODE_ENV=production

# Expose port 3000
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
