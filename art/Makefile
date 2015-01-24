.SILENT:

define render
inkscape -e $@ -C -h $(SIZE) -w $(SIZE) $< >/dev/null
endef

.PHONY: all
all: logo_xlarge.png logo_large.png logo_medium.png logo_small.png logo_gnome.png logo_xsmall.png

logo_xlarge.png: logo.svg
	$(eval SIZE=256)
	$(render)
logo_large.png: logo.svg
	$(eval SIZE=48)
	$(render)
logo_medium.png: logo.svg
	$(eval SIZE=32)
	$(render)
logo_small.png: logo.svg
	$(eval SIZE=22)
	$(render)
logo_gnome.png: logo.svg
	$(eval SIZE=24)
	$(render)
logo_xsmall.png: logo.svg
	$(eval SIZE=16)
	$(render)
