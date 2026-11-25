import api from 'services/apiConfig';

export const EVENT_PAGE_SIZE = 5;
export const EVENT_MAX = 20;

// Lấy các sự kiện cộng đồng từ hôm nay trở đi (backend tính theo giờ Việt Nam)
export const fetchUpcomingEvents = async (limit = EVENT_PAGE_SIZE) => {
  const response = await api.get('/events/upcoming', { params: { limit } });
  return Array.isArray(response.data) ? response.data : [];
};

// "2026-11-28" -> "28/11/2026"
export const formatEventDate = (isoDate) => {
  if (!isoDate) return '';
  const [year, month, day] = isoDate.split('-');
  return `${day}/${month}/${year}`;
};

// "18:00:00" -> "18:00"
export const formatEventTime = (time) => (time ? time.slice(0, 5) : '');
