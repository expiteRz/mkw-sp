#include "FontManager.h"

#include <revolution.h>

static void FontManager_initFont(FontManager *this, u32 index, const char *file) {
    this->fonts[index] = new(sizeof(Font));
    Font_ct(this->fonts[index]);
    Font_load(this->fonts[index], file);
}

static void my_FontManager_init(FontManager *this) {
    switch (SCGetLanguage()) {
    case SC_LANG_KOREAN:
        FontManager_initFont(this, 0, "tt_kart_font_rodan_ntlg_pro_b_K.brfnt");
        break;
    default:
        FontManager_initFont(this, 0, "tt_kart_font_rodan_ntlg_pro_b_R.brfnt");
        break;
    }
    switch (SCGetLanguage()) {
    case SC_LANG_KOREAN:
        FontManager_initFont(this, 1, "kart_font_K.brfnt");
        break;
    default:
        FontManager_initFont(this, 1, "kart_font_R.brfnt");
        break;
    }
    FontManager_initFont(this, 2, "tt_kart_extension_font.brfnt");
    FontManager_initFont(this, 3, "indicator_font.brfnt");
    FontManager_initFont(this, 4, "mario_font_number_red.brfnt");
    FontManager_initFont(this, 5, "mario_font_number_blue.brfnt");
}
PATCH_B(FontManager_init, my_FontManager_init);
