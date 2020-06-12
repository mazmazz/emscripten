#include <emscripten.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>

#define MIDI_PATH "/sound.mid"
#define SOUNDFONT_PATH "/soundfont.sf2"

Mix_Music *midi = NULL;

void sound_loop_then_quit() {
    if (Mix_Playing(-1))
        return;
    printf("Done audio\n");
    Mix_FreeMusic(midi);
    Mix_CloseAudio();

    emscripten_cancel_main_loop();
    printf("Shutting down\n");
#ifdef REPORT_RESULT
    REPORT_RESULT(1);
#endif
}

int main(int argc, char* argv[]){
    if (SDL_Init(SDL_INIT_AUDIO) < 0)
        return -1;
    int const frequency = EM_ASM_INT_V({
        var context;
        try {
            context = new AudioContext();
        } catch (e) {
            context = new webkitAudioContext(); // safari only
        }
        return context.sampleRate;
    });
    if(Mix_OpenAudio(frequency, MIX_DEFAULT_FORMAT, 2, 1024) == -1)
        return -1;
    midi = Mix_LoadMUS(MIDI_PATH);
    if (midi == NULL)
        return -1;
    if (!Mix_SetSoundFonts(SOUNDFONT_PATH))
        return -1;
    if (Mix_PlayMusic(midi, 0) == -1)
        return -1;
    // Ensure that the test gives an error if MIDI support was not compiled into SDL2_Mixer.
    if (Mix_Init(MIX_INIT_FLUIDSYNTH) == -1)
        return -1;
    printf("Starting sound play loop\n");
    emscripten_set_main_loop(sound_loop_then_quit, 0, 1);
    return 0;
}
