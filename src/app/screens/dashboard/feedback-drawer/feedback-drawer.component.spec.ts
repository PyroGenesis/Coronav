import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FeedbackDrawerComponent } from './feedback-drawer.component';

describe('FeedbackDrawerComponent', () => {
  let component: FeedbackDrawerComponent;
  let fixture: ComponentFixture<FeedbackDrawerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FeedbackDrawerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FeedbackDrawerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
