dotenv.config();

const config = {
    ENVIRONMENT: process.env.ENVIRONMENT || 'dev',
    BASE_URL: process.env.BASE_URL || 'http://localhost:8000',
    API_URL: process.env.API_URL || 'http://localhost:8000/api',
};

export default config;
