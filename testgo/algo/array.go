package algo

type array struct {
	data []int
	size uint
}

func (g *array) grow() {}

func (g *array) add() {}

func New() *array {
	return &array{
		data: make([]int, 0),
	}
}

func (g *array) Add(i int) {

}

func (g *array) Get(i int) {}

func (g *array) Set() {}

func (g *array) Size() int {
	return 0
}
