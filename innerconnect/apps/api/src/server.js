const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { createServer } = require('http');
const { Server } = require('socket.io');
const { port } = require('./config/env');

const authRoutes = require('./routes/authRoutes');
const matchRoutes = require('./routes/matchRoutes');
const adminRoutes = require('./routes/adminRoutes');

const app = express();
app.use(helmet());
app.use(cors({ origin: true, credentials: true }));
app.use(express.json({ limit: '2mb' }));

app.get('/health', (_, res) => res.json({ status: 'ok', service: 'innerconnect-api' }));
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/matching', matchRoutes);
app.use('/api/v1/admin', adminRoutes);

const server = createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
  socket.on('chat:message', (payload) => {
    io.to(payload.matchId).emit('chat:message', payload);
  });

  socket.on('chat:join', (matchId) => socket.join(matchId));
});

server.listen(port, () => {
  console.log(`InnerConnect API running on port ${port}`);
});
