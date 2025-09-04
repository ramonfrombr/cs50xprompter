# Use official Node.js LTS as base image
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and lock files
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install dependencies
RUN npm ci

# Copy the rest of the source code
COPY . .

# Build-time argument for backend URL
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Build the Next.js app
RUN npm run build

# -------------------------------------------
# Production image
FROM node:20-alpine AS runner

WORKDIR /app

# Copy package.json and install only production deps
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN npm ci --omit=dev

# Copy built files from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Expose port
EXPOSE 3000

# Set NODE_ENV
ENV NODE_ENV=production

# Runtime environment variable (ensure frontend uses correct backend URL)
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Start the Next.js app
CMD ["npm", "start"]
