package dev.foss.goldenpath.ui.feedback

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.TextButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import dev.foss.goldenpath.R
import dev.foss.goldenpath.display.highRefreshScroll
import dev.foss.goldenpath.feedback.FeedbackPreview
import dev.foss.goldenpath.githubfeedback.IssueFormUrl
import dev.foss.goldenpath.ui.insets.bottomInsetPadding
import dev.foss.goldenpath.ui.theme.SpacingMd
import kotlinx.coroutines.launch

@Composable
fun FeedbackScreen(
    kind: String,
    releaseRepo: String,
    stack: String?,
    onBack: () -> Unit,
    snackbarHostState: SnackbarHostState? = null,
    scrollY: Int = 0,
    onScroll: (Int) -> Unit = {},
    modifier: Modifier = Modifier,
) {
    var description by remember { mutableStateOf("") }
    var copiedVisible by remember { mutableStateOf(false) }
    var confirmDiscard by remember { mutableStateOf(false) }
    val preview = FeedbackPreview.text(kind, description, stack)
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val canSubmit = FeedbackPreview.canSubmit(description, stack)
    val copiedMsg = stringResource(R.string.feedback_copied)
    val scrollState = rememberScrollState(initial = scrollY)
    LaunchedEffect(scrollState.value) { onScroll(scrollState.value) }
    Column(
        modifier = modifier
            .testTag("feedback-panel")
            .highRefreshScroll()
            .verticalScroll(scrollState)
            .padding(SpacingMd),
        verticalArrangement = Arrangement.spacedBy(SpacingMd),
    ) {
        Text(
            text = stringResource(
                if (kind == "feature") R.string.feedback_feature_title else R.string.feedback_bug_title,
            ),
            style = MaterialTheme.typography.headlineSmall,
        )
        Text(text = stringResource(R.string.feedback_clipboard_hint))
        OutlinedTextField(
            value = description,
            onValueChange = { description = it },
            label = { Text(stringResource(R.string.feedback_description)) },
            modifier = Modifier.testTag("feedback-description"),
        )
        Text(text = preview, style = MaterialTheme.typography.bodySmall, modifier = Modifier.testTag("feedback-preview"))
        Button(
            onClick = {
                clipboard.setText(AnnotatedString(preview))
                copiedVisible = true
                if (snackbarHostState != null) {
                    scope.launch { snackbarHostState.showSnackbar(copiedMsg) }
                }
            },
            modifier = Modifier.testTag("feedback-copy"),
        ) {
            Text(stringResource(R.string.feedback_copy))
        }
        if (copiedVisible) {
            Text(
                text = copiedMsg,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.testTag("feedback-copied"),
            )
        }
        Button(
            enabled = canSubmit,
            onClick = {
                val template = if (kind == "feature") "product_idea.yml" else "bug_report.yml"
                val fields = if (kind == "feature") {
                    mapOf("problem" to description, "solution" to preview, "title" to "[feat]: ")
                } else {
                    mapOf("description" to description, "reproduction" to preview, "title" to "[bug]: ")
                }
                val built = IssueFormUrl.build(releaseRepo, template, fields)
                if (built.bodyTooLarge) {
                    clipboard.setText(AnnotatedString(built.clipboardMarkdown ?: preview))
                }
                val url = built.url
                if (url.startsWith("https://")) {
                    runCatching {
                        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                    }
                }
            },
        ) {
            Text(stringResource(R.string.feedback_open))
        }
        Button(
            onClick = { confirmDiscard = true },
            modifier = Modifier.bottomInsetPadding().testTag("feedback-discard"),
        ) {
            Text(stringResource(R.string.feedback_discard))
        }
        if (confirmDiscard) {
            AlertDialog(
                onDismissRequest = { confirmDiscard = false },
                title = { Text(stringResource(R.string.feedback_discard_confirm)) },
                confirmButton = {
                    TextButton(
                        onClick = {
                            clipboard.setText(AnnotatedString(""))
                            confirmDiscard = false
                            onBack()
                        },
                        modifier = Modifier.testTag("feedback-discard-confirm"),
                    ) {
                        Text(stringResource(R.string.feedback_discard_confirm_yes))
                    }
                },
                dismissButton = {
                    TextButton(
                        onClick = { confirmDiscard = false },
                        modifier = Modifier.testTag("feedback-discard-cancel"),
                    ) {
                        Text(stringResource(R.string.feedback_discard_confirm_no))
                    }
                },
            )
        }
    }
}
