#version 430
out vec4 fragColor;
in vertexData
{
	vec2 uv;
} vertexIn;
uniform sampler2D ts;
void main()
{
	fragColor = texture(ts, vertexIn.uv);
};