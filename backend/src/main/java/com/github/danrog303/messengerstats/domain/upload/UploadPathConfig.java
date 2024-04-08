package com.github.danrog303.messengerstats.domain.upload;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

@Configuration
@AllArgsConstructor
public class UploadPathConfig {

    private final UploadPathHandler handler;

    @Bean
    public RouterFunction<ServerResponse> UploadRouter(){
     return RouterFunctions.route()
             .POST("upload", handler::fileUpload)
             .build();
    }
}
