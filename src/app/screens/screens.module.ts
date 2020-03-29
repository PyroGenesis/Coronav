import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FormsModule } from '@angular/forms';

import { MatSliderModule } from '@angular/material/slider';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatBottomSheetModule } from '@angular/material/bottom-sheet';
import { FeedbackDrawerComponent } from './dashboard/feedback-drawer/feedback-drawer.component';
import { MatListModule } from '@angular/material/list';
import { MatSnackBarModule, MAT_SNACK_BAR_DEFAULT_OPTIONS } from '@angular/material/snack-bar';
import { MatSelectModule } from '@angular/material/select';



@NgModule({
  declarations: [DashboardComponent, FeedbackDrawerComponent],
  imports: [
    CommonModule,
    FormsModule,
    MatSliderModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatBottomSheetModule,
    MatListModule,
    MatSnackBarModule,
    MatSelectModule
  ],
  exports: [ DashboardComponent ],
  // providers: [{provide: MAT_SNACK_BAR_DEFAULT_OPTIONS, useValue: {verticalPosition: 'top'}}]
})
export class ScreensModule { }
