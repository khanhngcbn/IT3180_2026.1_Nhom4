import React, { useEffect, useState } from 'react';
import {
  Box,
  SimpleGrid,
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  FormLabel,
  useColorModeValue,
  Image,
  Icon,
} from '@chakra-ui/react';
import { InfoIcon, CheckCircleIcon, CalendarIcon, StarIcon } from '@chakra-ui/icons';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
// Adjust paths as needed
import playImg from '../../../assets/img/play.jpg';
import gymImg from '../../../assets/img/gym.jpg';
import poolImg from '../../../assets/img/pool.jpg';
import {
  EVENT_MAX,
  EVENT_PAGE_SIZE,
  fetchUpcomingEvents,
  formatEventDate,
  formatEventTime,
} from 'services/eventService';

const HomePage = () => {
  const textColor = useColorModeValue('gray.800', 'white');
  const tableHeaderBg = useColorModeValue('blue.600', 'blue.800');
  const tableHeaderColor = useColorModeValue('white', 'gray.200');
  const hoverBg = useColorModeValue('gray.100', 'gray.700');
  const [events, setEvents] = useState([]);
  const [eventLimit, setEventLimit] = useState(EVENT_PAGE_SIZE);
  const [eventsLoading, setEventsLoading] = useState(false);
  const [eventsError, setEventsError] = useState('');

  useEffect(() => {
    let cancelled = false;
    setEventsLoading(true);
    fetchUpcomingEvents(eventLimit)
      .then((data) => {
        if (!cancelled) {
          setEvents(data);
          setEventsError('');
        }
      })
      .catch(() => {
        if (!cancelled) setEventsError('Không tải được danh sách sự kiện.');
      })
      .finally(() => {
        if (!cancelled) setEventsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [eventLimit]);

  return (
    <Box minH="100vh" bg="gray.100" py={8} px={4} mt={16}>
      <SimpleGrid columns={{ base: 1, md: 2 }} templateColumns={{ base: '1fr', md: '3fr 1fr' }} spacing={6} maxW="1200px" mx="auto">
        {/* Introduction Section with Images */}
        <Box gridColumn={{ base: '1 / -1', md: '1 / -1' }} bg="white" borderRadius="2xl" shadow="lg" p={6}>
          <FormLabel
            display="flex"
            ms="4px"
            fontSize="sm"
            fontWeight="500"
            color={textColor}
            mb="8px"
            justifyContent="center"
            alignItems="center"
          >
            <Icon as={InfoIcon} w={6} h={6} mr={2} color="blue.500" />
            <Text fontSize="2xl" fontWeight="700">
              Giới thiệu về BlueMoon
            </Text>
          </FormLabel>
          <Text color="gray.600" lineHeight="relaxed" mb={4}>
            Chung cư <strong>BlueMoon</strong> là một khu dân cư hiện đại tọa lạc tại trung tâm thành phố, được thiết kế để mang lại cuộc sống tiện nghi và đẳng cấp cho cư dân. Được thành lập vào năm 2015, BlueMoon đã trở thành biểu tượng của sự sang trọng và thân thiện với môi trường.
            <br /><br />
            <strong>Tính năng nổi bật:</strong>
            <Box as="ul" pl={6} listStyleType="none">
              <li>
                <Box display="flex" alignItems="center">
                  <Icon as={CheckCircleIcon} w={4} h={4} mr={2} color="green.500" />
                  Hệ thống an ninh 24/7 với camera giám sát và đội ngũ bảo vệ chuyên nghiệp.
                </Box>
              </li>
              <li>
                <Box display="flex" alignItems="center">
                  <Icon as={CheckCircleIcon} w={4} h={4} mr={2} color="green.500" />
                  Khu vui chơi trẻ em, phòng gym, hồ bơi và công viên xanh ngay trong khuôn viên.
                </Box>
              </li>
              <li>
                <Box display="flex" alignItems="center">
                  <Icon as={CheckCircleIcon} w={4} h={4} mr={2} color="green.500" />
                  Hệ thống quản lý tòa nhà thông minh, hỗ trợ cư dân qua ứng dụng di động.
                </Box>
              </li>
              <li>
                <Box display="flex" alignItems="center">
                  <Icon as={CheckCircleIcon} w={4} h={4} mr={2} color="green.500" />
                  Gần các tiện ích công cộng như trường học, bệnh viện và trung tâm thương mại.
                </Box>
              </li>
            </Box>
            <br />
            <strong>Lịch sử:</strong> BlueMoon được phát triển bởi tập đoàn bất động sản hàng đầu, với mục tiêu tạo ra một cộng đồng bền vững và gắn kết. Qua nhiều năm, chúng tôi đã tổ chức hàng loạt sự kiện cộng đồng để tăng cường sự kết nối giữa các cư dân.
            <br /><br />
            <strong>Địa chỉ:</strong> Số 1 trong lòng Thái, đường Đại Cồ Việt, Hà Nội, Việt Nam.
          </Text>
          <SimpleGrid columns={3} spacing={4} mb={4}>
            <Image
              src={playImg}
              alt="Play Area"
              borderRadius="lg"
              maxW="100%"
              maxH="200px"
              _hover={{ transform: 'scale(1.05)', transition: 'transform 0.3s ease-in-out' }}
            />
            <Image
              src={gymImg}
              alt="Gym"
              borderRadius="lg"
              maxW="100%"
              maxH="200px"
              _hover={{ transform: 'scale(1.05)', transition: 'transform 0.3s ease-in-out' }}
            />
            <Image
              src={poolImg}
              alt="Pool"
              borderRadius="lg"
              maxW="100%"
              maxH="200px"
              _hover={{ transform: 'scale(1.05)', transition: 'transform 0.3s ease-in-out' }}
            />
          </SimpleGrid>
          <Box mt={4} textAlign="center">
            <Button
              variant="darkBrand"
              color="white"
              fontSize="sm"
              fontWeight="500"
              borderRadius="10px"
              px="15px"
              py="5px"
            >
              Tìm hiểu thêm
            </Button>
          </Box>
        </Box>

        {/* Events Section */}
        <Box bg="white" borderRadius="2xl" shadow="lg" p={6} gridColumn={{ md: '1 / 2', base: '1 / -1' }}>
          <FormLabel
            display="flex"
            ms="4px"
            fontSize="sm"
            fontWeight="500"
            color={textColor}
            mb="8px"
            justifyContent="center"
            alignItems="center"
          >
            <Icon as={StarIcon} w={6} h={6} mr={2} color="yellow.500" />
            <Text fontSize="2xl" fontWeight="700">
              Sự kiện sắp tới
            </Text>
          </FormLabel>
          <Box overflowX="auto" maxH="400px" overflowY="auto">
            <Table variant="simple">
              <Thead bg={tableHeaderBg}>
                <Tr>
                  <Th color={tableHeaderColor} p={4}>Ngày</Th>
                  <Th color={tableHeaderColor} p={4}>Sự kiện</Th>
                  <Th color={tableHeaderColor} p={4}>Mô tả</Th>
                </Tr>
              </Thead>
              <Tbody>
                {events.length === 0 && (
                  <Tr>
                    <Td p={4} colSpan={3} textAlign="center" color="gray.500">
                      {eventsLoading ? 'Đang tải sự kiện...' : eventsError || 'Chưa có sự kiện sắp tới.'}
                    </Td>
                  </Tr>
                )}
                {events.map((event) => (
                  <Tr
                    key={`${event.date}-${event.title}`}
                    _hover={{ bg: hoverBg, transform: 'translateY(-2px)', transition: 'all 0.2s ease-in-out' }}
                    transition="all 0.2s ease-in-out"
                  >
                    <Td p={4}>
                      <Box display="flex" alignItems="center">
                        <Icon as={CalendarIcon} w={4} h={4} mr={2} color="blue.500" />
                        <Box>
                          <Text>{formatEventDate(event.date)}</Text>
                          <Text fontSize="sm" color="gray.500">{formatEventTime(event.time)}</Text>
                        </Box>
                      </Box>
                    </Td>
                    <Td p={4}>{event.title}</Td>
                    <Td p={4}>{event.description}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
          <Box mt={4} textAlign="center">
            <Button
              variant="darkBrand"
              color="white"
              fontSize="sm"
              fontWeight="500"
              borderRadius="10px"
              px="15px"
              py="5px"
              isLoading={eventsLoading}
              isDisabled={eventLimit >= EVENT_MAX}
              onClick={() => setEventLimit((limit) => Math.min(limit + EVENT_PAGE_SIZE, EVENT_MAX))}
            >
              Xem thêm sự kiện
            </Button>
          </Box>
        </Box>

        {/* Calendar Section */}
        <Box bg="white" borderRadius="2xl" shadow="lg" p={6} gridColumn={{ md: '2 / 3', base: '1 / -1' }}>
          <FormLabel
            display="flex"
            ms="4px"
            fontSize="sm"
            fontWeight="500"
            color={textColor}
            mb="8px"
            justifyContent="center"
            alignItems="center"
          >
            <Icon as={CalendarIcon} w={6} h={6} mr={2} color="blue.500" />
            <Text fontSize="2xl" fontWeight="700">
              Lịch BlueMoon
            </Text>
          </FormLabel>
          <Box display="flex" justifyContent="center">
            <Calendar
              className="shadow-md rounded-lg"
              tileClassName="text-center"
            />
          </Box>
        </Box>
      </SimpleGrid>
    </Box>
  );
};

export default HomePage;