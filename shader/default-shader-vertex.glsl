#version 430
layout (location = 0) in vec3 vertex;
layout (location = 1) in vec2 uv;
uniform mat4 mvp;
out vertexData
{
	vec2 uv;
} vertexOut;
void main()
{
	vertexOut.uv = uv + vec2(uvMove, 0);
	gl_Position = mvpm * vec4(vertex, 1.0);
}