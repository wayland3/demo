package sort_func

func Quick(s []int, l, r int) {
	if l >= r {
		return
	}

	left := l
	right := r
	pivot := s[l]

	for left < right {
		for right > left && s[right] >= pivot {
			right--
		}

		if left < right {
			s[left] = s[right]
		}

		for right > left && s[left] <= pivot {
			left++
		}

		if left < right {
			s[right] = s[left]
		}

		if left >= right {
			s[left] = pivot
		}

		Quick(s, l, right-1)
		Quick(s, right+1, r)
	}
}

func Quick2() {}
