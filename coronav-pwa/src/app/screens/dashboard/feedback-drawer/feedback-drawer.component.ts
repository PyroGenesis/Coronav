import { Component, OnInit, Inject } from '@angular/core';
import { MatBottomSheetRef, MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';

@Component({
  selector: 'app-feedback-drawer',
  templateUrl: './feedback-drawer.component.html',
  styleUrls: ['./feedback-drawer.component.scss']
})
export class FeedbackDrawerComponent implements OnInit {

  constructor(private selfReference: MatBottomSheetRef<FeedbackDrawerComponent>, @Inject(MAT_BOTTOM_SHEET_DATA) public data: any) {
    console.log('data', data);
  }

  ngOnInit(): void {
  }

  dismiss() {
    this.selfReference.dismiss();
  }

}
