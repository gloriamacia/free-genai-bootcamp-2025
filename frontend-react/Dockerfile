# Stage 1: Build the frontend using Node
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the built files with Nginx
FROM nginx:stable-alpine
# Copy the build output from the previous stage.
COPY --from=build /app/dist /usr/share/nginx/html
# Copy your custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

