package com.example.demo.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.demo.dto.ContributionTypeDTO;
import com.example.demo.entity.ContributionType;
import com.example.demo.entity.User;
import com.example.demo.repository.ContributionTypeRepository;
import com.example.demo.repository.UserRepository;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ContributionTypeServiceTest {

    @Mock
    private ContributionTypeRepository contributionTypeRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private ContributionTypeService contributionTypeService;

    @Test
    void createContributionType_persistsActiveTypeAndMapsCreatorName() {
        User creator = new User();
        creator.setId(10L);
        creator.setName("Admin User");

        ContributionTypeDTO input = new ContributionTypeDTO();
        input.setName("Charity Fund");
        input.setDescription("Annual charity drive");

        when(userRepository.findById(10L)).thenReturn(Optional.of(creator));
        when(contributionTypeRepository.save(any(ContributionType.class))).thenAnswer(invocation -> {
            ContributionType saved = invocation.getArgument(0);
            saved.setId(1L);
            return saved;
        });

        ContributionTypeDTO result = contributionTypeService.createContributionType(input, 10L);

        assertEquals(1L, result.getId());
        assertEquals("Charity Fund", result.getName());
        assertEquals("Admin User", result.getCreatedByName());
        assertTrue(result.getIsActive());
    }

    @Test
    void createContributionType_throwsWhenUserNotFound() {
        ContributionTypeDTO input = new ContributionTypeDTO();
        input.setName("Charity Fund");

        when(userRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class,
                () -> contributionTypeService.createContributionType(input, 99L));
    }

    @Test
    void deleteContributionType_softDeletesBySettingInactive() {
        ContributionType existing = new ContributionType();
        existing.setId(5L);
        existing.setName("Old Fund");
        existing.setIsActive(true);

        when(contributionTypeRepository.findById(5L)).thenReturn(Optional.of(existing));

        contributionTypeService.deleteContributionType(5L);

        assertFalse(existing.getIsActive());
        verify(contributionTypeRepository).save(existing);
    }

    @Test
    void getActiveContributionTypes_returnsOnlyActiveDtos() {
        ContributionType active = new ContributionType();
        active.setId(2L);
        active.setName("Maintenance");
        active.setIsActive(true);

        when(contributionTypeRepository.findByIsActive(true)).thenReturn(List.of(active));

        List<ContributionTypeDTO> result = contributionTypeService.getActiveContributionTypes();

        assertEquals(1, result.size());
        assertEquals("Maintenance", result.get(0).getName());
    }
}
