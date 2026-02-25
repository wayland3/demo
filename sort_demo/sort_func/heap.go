package sort_func

import "log"

// 节点i的左子为2i+1,右子为2i+2
// 节点i的父为(i-1)/2
// i>n/2-1 叶子

type Heap []int

func (h Heap) swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h Heap) less(i, j int) bool {
	return h[i] < h[j]
}

func (h *Heap) Push(n int) {
	*h = append(*h, n)
	h.up(len(*h) - 1)
}

func (h Heap) up(i int) {
	for {
		// 父节点比较
		p := (i - 1) / 2
		if p == i || h.less(p, i) {
			break
		}
		h.swap(i, p)
		i = p
	}
}

func (h Heap) down(i int) {
	log.Println(len(h))
	for {
		// 是否是叶子
		l := 2*i + 1 // 左子
		if l > len(h)-1 {
			break
		}

		// 最小的子节点 初始左子
		cMin := l
		// 是否有右子
		if r := l + 1; r < len(h)-1 && h.less(r, l) {
			cMin = r
		}

		if h.less(i, cMin) {
			break
		}

		h.swap(i, cMin)
		i = cMin // 继续dwon
	}

}

func (h *Heap) Remove(i int) (int, bool) {
	maxIdx := len(*h) - 1
	// 判断删除合法
	if i < 0 || i > maxIdx {
		return 0, false
	}

	n := (*h)[i]
	// 删除位与最末尾交换, 删除末尾
	h.swap(i, maxIdx)
	*h = (*h)[:maxIdx]

	// 向下移动 / 上
	if (*h)[i] > (*h)[(i-1)/2] {
		h.down(i)
	} else {
		h.up(i)
	}
	return n, true
}

// remove(0)
func (h *Heap) Pop() (int, bool) {
	maxIdx := len(*h) - 1
	if maxIdx == -1 {
		return 0, false
	}

	n := (*h)[0]
	// 删除位与最末尾交换, 删除末尾
	h.swap(0, maxIdx)
	*h = (*h)[:maxIdx]
	h.down(0)
	return n, true
}

func (h Heap) Init() {
	n := len(h)
	// i > n/2-1 的结点为叶子结点本身已经是堆了
	for i := n/2 - 1; i >= 0; i-- {
		h.down(i)
	}
}
