#version 330 core

out vec4 fragColor;

in vec2 uv_0;
in vec3 v_normal;
in vec3 v_fragPos;
in vec3 frag_color;

uniform sampler2D tex_0;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 viewPos;
uniform float ambient;
uniform float shininess;

void main() {
    vec3 norm = normalize(v_normal);
    vec3 lightDir = normalize(lightPos - v_fragPos);
    vec3 viewDir = normalize(viewPos - v_fragPos);

    float diff = max(dot(norm, lightDir), 0.0);

    vec3 ambient = ambient * lightColor;

    vec3 diffuse = diff * lightColor;

    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = spec * lightColor;

    vec3 lighting = (ambient + diffuse + specular) * frag_color;

    vec4 tex_color = texture(tex_0, uv_0);

    vec3 finalColor = tex_color.rgb * lighting;

    fragColor = vec4(finalColor, 1.0);
}
