/*
Copyright The Velero Contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package cli

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/vmware-tanzu/velero/pkg/cmd/util/flag"
)

func TestCompleteOfSelectOption(t *testing.T) {
	option := &SelectOptions{}
	args := []string{"arg1", "arg2"}
	require.NoError(t, option.Complete(args))
	assert.Equal(t, args, option.Names)
}

func TestValidateOfSelectOption(t *testing.T) {
	option := &SelectOptions{
		Names:    nil,
		Selector: flag.LabelSelector{},
		All:      false,
	}
	require.Error(t, option.Validate())

	option.All = true
	assert.NoError(t, option.Validate())
}
