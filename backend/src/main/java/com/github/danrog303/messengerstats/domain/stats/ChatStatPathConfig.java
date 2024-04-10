package com.github.danrog303.messengerstats.domain.stats;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
@RequiredArgsConstructor
public class ChatStatPathConfig {
    private final ChatStatPathHandler pathHandlerService;

    @Bean
    public RouterFunction<ServerResponse> statsRouter() {
        return RouterFunctions.route()
                .GET("stats/{dataFileKey}", pathHandlerService::getMessengerStatistics)
                .build();
    }
}
