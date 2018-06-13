import shuffle = require("shuffle-array");

export default class Decker {
    deckList: string[]

    constructor() {
        this.deckList = []
    }

    shuffle() {
        const color = ['r', 'g', 'b', 'y']
        for (let c of color) {
            for (let i=1; i <= 9; i++) {
                this.deckList.push(c + String(i))
            }
        }
        this.deckList = shuffle(this.deckList)
    }

    pop(): string {
        if (this.deckList.length === 0) {
            this.shuffle()
        }
        const deck = String(this.deckList.pop())
        return deck
    }

    pops(n: number): string[] {
        const rt: string[] = []
        for (let i = 0; i < n; i++) {
            rt.push(this.pop())
        }
        return rt
    }

}