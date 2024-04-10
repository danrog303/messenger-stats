package com.github.danrog303.messengerstats.domain.stats;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Map;

@Data
@AllArgsConstructor
public class ChatStatEntry {
    private String type;
    private Map<String, Long> metrics;
}
