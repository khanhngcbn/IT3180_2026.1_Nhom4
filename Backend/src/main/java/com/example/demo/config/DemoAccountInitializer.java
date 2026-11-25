package com.example.demo.config;

import com.example.demo.dto.ManualUserDTO;
import com.example.demo.entity.User;
import com.example.demo.enums.ResidentStatus;
import com.example.demo.repository.UserRepository;
import com.example.demo.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Tạo sẵn tài khoản mẫu cho từng vai trò để kiểm thử (Kế toán, cư dân, tài khoản bị khóa).
 * Chỉ tạo tài khoản chưa tồn tại, nên chạy lại nhiều lần không bị trùng.
 * Tắt khi triển khai thật bằng biến môi trường SEED_DEMO_ACCOUNTS=false.
 * Danh sách tài khoản và mật khẩu được ghi trong README (mục "Tài khoản mẫu").
 */
@Component
@Order(2)
public class DemoAccountInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DemoAccountInitializer.class);

    private record DemoAccount(String username, String password, String role, String fullName, long age,
                               String phone, String email, Set<String> apartments, ResidentStatus status,
                               boolean active) {
    }

    static final List<DemoAccount> ACCOUNTS = List.of(
            new DemoAccount("ketoan", "Ketoan@123", "ADMIN", "Nguyễn Thị Ngân", 35,
                    "0901000002", "ketoan@bluemoon.test", Set.of(), ResidentStatus.THUONGTRU, true),
            new DemoAccount("cudan01", "Cudan01@123", "USER", "Trần Minh An", 42,
                    "0901000003", "cudan01@bluemoon.test", Set.of("A0012"), ResidentStatus.THUONGTRU, true),
            new DemoAccount("cudan02", "Cudan02@123", "USER", "Lê Thu Hà", 29,
                    "0901000004", "cudan02@bluemoon.test", Set.of("A0023", "A0024"), ResidentStatus.TAMTRU, true),
            new DemoAccount("cudankhoa", "Cudankhoa@123", "USER", "Phạm Văn Khóa", 50,
                    "0901000005", "cudankhoa@bluemoon.test", Set.of(), ResidentStatus.TAMVANG, false)
    );

    @Value("${app.seed.demo-accounts:true}")
    private boolean enabled;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserService userService;

    @Override
    public void run(String... args) {
        if (!enabled) {
            return;
        }
        for (DemoAccount account : ACCOUNTS) {
            if (userRepository.existsByName(account.username())) {
                continue;
            }
            try {
                create(account);
                log.info("Đã tạo tài khoản mẫu '{}' ({})", account.username(), account.role());
            } catch (RuntimeException e) {
                log.warn("Bỏ qua tài khoản mẫu '{}': {}", account.username(), e.getMessage());
            }
        }
    }

    private void create(DemoAccount account) {
        ManualUserDTO dto = new ManualUserDTO();
        dto.setName(account.username());
        dto.setPassword(account.password());
        dto.setRole(account.role());
        dto.setFullName(account.fullName());
        dto.setAge(account.age());
        dto.setPhone(account.phone());
        dto.setEmail(account.email());
        dto.setApartmentNumbers(new HashSet<>(account.apartments()));
        dto.setStatus(account.status());
        userService.addUser(dto);

        if (!account.active()) {
            User user = userRepository.findByName(account.username());
            user.setActivation(false);
            userRepository.save(user);
        }
    }
}
