package main

import "log"

func longestCommonPrefix(strs []string) string {
	if strs == nil {
		return ""
	}

	strsLen := len(strs)
	if strsLen == 1 {
		return strs[0]
	}

	preLeft := longestCommonPrefix(strs[:strsLen/2])
	preRight := longestCommonPrefix(strs[strsLen/2:])

	common := -1
	for i, j := 0, 0; i < len(preLeft) && j < len(preRight) && preLeft[i] == preRight[i]; i, j, common = i+1, j+1, common+1 {
	}
	return preLeft[:common+1]
}

func main() {
	strs := []string{"abc", "abcd", "abcc", "adca"}
	log.Println(longestCommonPrefix(strs))
}

func b(i int) (ii int) {
	ii = 1
	if i == 1 {
		return
	} else if i == 2 {
		return
	} else if i == 3 {
		return
	} else if i == 4 {
		return
	} else if i == 5 {
		return
	} else if i == 6 {
		return
	} else if i == 7 {
		return
	} else if i == 8 {
		return
	} else if i == 9 {
		return
	} else if i == 10 {
		return
	} else if i == 11 {
		return
	} else if i == 12 {
		return
	} else if i == 13 {
		return
	} else if i == 14 {
		return
	}
	return
}
