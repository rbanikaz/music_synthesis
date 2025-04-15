# 🎵 Music Synthesis Project

**A hands-on exploration of musical notes, waveforms, and sound visualization.**

🌐 **[Try it here!](https://music-rbanikaz.pythonanywhere.com/)**

---

## 🚀 Overview

This project allows you to:

- **Play specific notes** for a fixed duration.
- **Play melodies** composed of sequences of notes.
- **Visualize waveforms** in real-time as audio streams from the server.
- **Explore** how different waveforms (sine, square, sawtooth, etc.) affect sound.

My daughter (currently 7.5 years old) and I used this tool to discover that high-pitched notes have higher frequencies, while lower-pitched notes have slower frequencies. And, of course, we had a lot of fun experimenting with various waveforms!

---

## 💡 Vibe Coding

This project is a clear example of **"vibe coding"**, a term I define as:

> *"The ability to productively generate working code for a problem space in which you have little to no expertise."*

Traditional software engineering usually requires a substantial amount of domain knowledge. For instance, efficiently generating audible sine waves in specific musical notes typically demands detailed knowledge about musical notation, frequency conversions, and audio libraries. Errors along the way can quickly become challenging without domain-specific insights. Just check out this [Wikipedia page on scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation) to get an idea of how complex this topic can be!

However, "vibe coding" enabled me to bypass extensive pre-existing domain knowledge and rapidly produce functional code through intuitive exploration and experimentation.

### Vibe Coding Tips:

These are personal reflections from my own experience — your mileage may vary.

1. **Start with Chat:** Most new ideas begin in Chat using models like GPT-4.5, o1, or o3-mini-high. For more ambitious or complex ideas, I switch to Deep Research mode.
2. **Use an Integrated Environment:** Once things move beyond simple scripts, tools like Cursor offer the most productive experience.
3. **Chat vs. Cursor:** While Cursor is great for diffs, sometimes I just want advice. In those moments, I often bounce back to ChatGPT for a more conversational approach.
4. **Reject the Diff (Sometimes):** I don’t blindly accept every suggested diff — I probably reject about 10% of them.
5. **Unexpected but Better:** It often implements things differently than I had planned. That’s not always bad — in many cases, it’s actually a better solution than what I originally had in mind.
6. **Stick to Your Patterns:** Sometimes it misses the design patterns I’m trying to follow. When that happens, I take back control, establish the pattern myself, and then return to the tool — after that, it usually catches on.


---

## 📖 Inspiration & Journey

Many years ago, in the late 1980s, I was a young boy fascinated by a piece of code on the Commodore 64 designed to play Beethoven’s *Für Elise*. I vividly remember spending hours trying to decipher and understand that mysterious code. While I continued to work extensively with computers throughout my life, music synthesis hadn't been something I revisited deeply.

Fast forward to today, prompted by a conversation with my piano-playing daughter, I revisited my early curiosity. Using ChatGPT, I started asking questions about music synthesis, quickly progressing from a simple Python script in Cursor to Jupyter notebooks, and finally building a fully functional web application.

It completely blows my mind that in fewer than 40 years, the complexity of music synthesis has transformed into something so accessible and straightforward. In just a few weekend hours, I created something that once seemed incredibly intricate.

---

## 🚧 The Paradigm Shift

We are living through an unprecedented revolution in software development unlike any that have come before (and there have been some big ones!). AI tools empower anyone with a bit of creativity and technical curiosity to bring complex ideas to life swiftly and effectively.

This is not just exciting—it’s revolutionary!

---

**Enjoy exploring music synthesis!** 🎶✨

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd music_synthesis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   python server.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```
